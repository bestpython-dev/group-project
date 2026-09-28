"""Email a student's grade report through Gmail SMTP.

Owned by: Aliyu Bappa  |  Branch: feature/ai-email-integration
"""

from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage

import streamlit as st

from Asher_Gbolahan.student import Student
from Asher_Gbolahan.student_manager import StudentManager
from Ismail_Muhammed.exceptions import EmailServiceError
from Ismail_Muhammed.safe_action import safe_action


def build_report(student: Student) -> str:
    return (
        f"Dear {student.get_name()},\n\n"
        "This is your current grade report from the Student Management System.\n\n"
        f"Student ID : {student.get_student_id()}\n"
        f"Course     : {student.get_course()}\n"
        f"Grade      : {student.get_grade()} ({student.letter_grade()})\n"
        f"Standing   : {student.standing()}\n"
        f"Pass mark  : {Student.PASS_MARK}\n\n"
        "If you have questions about this result, please contact your course tutor.\n\n"
        "Kind regards,\n"
        "Academic Registry\n"
        "Student Management System\n"
    )


def send_grade_report(student: Student) -> None:
    sender = (os.getenv("GMAIL_ADDRESS") or "").strip()
    password = (os.getenv("GMAIL_APP_PASSWORD") or "").strip().replace(" ", "")
    if not sender or not password:
        raise EmailServiceError(
            "Gmail is not configured. Add GMAIL_ADDRESS and GMAIL_APP_PASSWORD to your .env file."
        )

    message = EmailMessage()
    message["Subject"] = f"Grade report — {student.get_name()} ({student.get_student_id()})"
    message["From"] = sender
    message["To"] = student.get_email()
    message.set_content(build_report(student))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=25) as smtp:
            smtp.login(sender, password)
            smtp.send_message(message)
    except smtplib.SMTPAuthenticationError as exc:
        raise EmailServiceError(
            "Gmail rejected the login. Use a Gmail App Password, not your ordinary account password."
        ) from exc
    except smtplib.SMTPException as exc:
        raise EmailServiceError("The email server could not send this report.") from exc


def render_email_report(manager: StudentManager) -> None:
    configured = bool(
        (os.getenv("GMAIL_ADDRESS") or "").strip() and (os.getenv("GMAIL_APP_PASSWORD") or "").strip()
    )
    if configured:
        st.success(f"Sending from {os.getenv('GMAIL_ADDRESS')} via Gmail SMTP.")
    else:
        st.info(
            "Email sending needs GMAIL_ADDRESS and GMAIL_APP_PASSWORD in `.env`. "
            "You can still preview the report below."
        )

    students = manager.get_all()
    if not students:
        st.info("Add a student before sending a grade report.")
        return

    labels = {f"{item.get_student_id()} — {item.get_name()}": item for item in students}
    picked = st.selectbox("Student", list(labels.keys()), key="email_picker")
    student = labels[picked]

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("Report preview")
    st.code(build_report(student), language="text")
    st.caption(f"Recipient: {student.get_email()}")
    if st.button("Email report to student", type="primary", use_container_width=True):
        ok, _, error = safe_action(send_grade_report, student)
        if ok:
            st.success(f"Grade report sent to {student.get_email()}.")
        else:
            st.error(error)
    st.markdown("</div>", unsafe_allow_html=True)
