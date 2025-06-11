from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models import Curso

bp = Blueprint('cursos', __name__)

