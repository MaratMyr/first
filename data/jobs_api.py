import flask

from . import db_session
from .jobs import Jobs
from flask import jsonify, make_response, request

blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 404)
    elif not all(key in request.json for key in
                 ['id', 'team_leader', 'job', 'work_size', 'collaborators',
                  'start_date', 'end_date']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    job = Jobs(
        id=request.json['id'],
        team_leader=request.json['team_leader'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        is_finished=request.json['is_finished']
    )
    if db_sess.query(Jobs).filter(Jobs.id == job.id).first():
        return jsonify({'error': 'id already exists'})
    db_sess.add(job)
    db_sess.commit()
    return jsonify({'id': job.id})



@blueprint.route('/api/jobs/<int: job_id>', methods=['POST'])
def edit_job(job_id):
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 404)
    elif not all(key in request.json for key in
                 ['id', 'team_leader', 'job', 'work_size', 'collaborators',
                  'start_date', 'end_date']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    job = Jobs(
        id=request.json['id'],
        team_leader=request.json['team_leader'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        start_date=request.json['start_date'],
        end_date=request.json['end_date'],
        is_finished=request.json['is_finished']
    )
    job_edit = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
    if not job_edit:
        return jsonify({'error': 'Not Found'})

    job_edit.id = job.id
    job_edit.team_leader = job.team_leader
    *****


    db_sess.commit()
    return jsonify({'id': job.id})