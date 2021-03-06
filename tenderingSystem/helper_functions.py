import os
from tenderingSystem import app
import secrets
from tenderingSystem import db
from sqlalchemy import extract
from tenderingSystem.model import Company
from flask_login import current_user


def save_tender_document(tender_document, sub_directory):
    random_name = secrets.token_hex(8)
    _, file_extension = os.path.splitext(tender_document.filename)
    file_name = random_name + file_extension
    path = os.path.join(app.root_path, 'uploads/' + sub_directory, file_name)
    tender_document.save(path)

    return file_name


def get_company_id():
    company = Company.query.filter_by(user=current_user.id).first()

    if company:
        return company.id


def get_company_information():
    company = Company.query.filter_by(user=current_user.id).first()

    return company


def return_path(sub_directory, file_name):
    return os.path.join(app.root_path, 'uploads/' + sub_directory, file_name)


def json_data(database_table, month, *condition):
    company = get_company_id()

    if company:
        result = db.session.query(database_table).filter_by(company=company).filter(
            extract('month', database_table.date_published) == month).count()

    return result


def check_duplicates(table_name, name_to_check_for):
    company = table_name.query.filter_by(company_name=name_to_check_for)

    return company
