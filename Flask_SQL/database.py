from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SecretKeyNotImportant'
#Specify the directory the SQLite db file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/acc/Desktop/vaelstmpredictor/Flask_SQL/DeepGenetics.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app, resources={r"/*": {"origins": "*"}}, allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials", "Access-Control-Allow-Origin", "Access-Control-Allow-Headers", "x-access-token"], supports_credentials=True)
db = SQLAlchemy(app)

class Chromosome(db.Model):
    __tablename__ = 'Chromosome'
    id = db.Column(db.Integer, primary_key=True)
    chromosomeID = db.Column(db.Integer, default = 0)
    generationID = db.Column(db.Integer, default = 0)
    fitness = db.Column(db.Float, default = 100)
    run_name = db.Column(db.String(50), default = 'dummy')
    predictor_type = db.Column(db.String(50), default = 'classification')
    batch_size = db.Column(db.Integer, default = 128)
    optimizer = db.Column(db.String(50), default = 'adam')
    num_epochs = db.Column(db.Integer, default = 200)
    dnn_weight = db.Column(db.Float, default = 1.0)
    vae_weight = db.Column(db.Float, default = 1.0)
    vae_kl_weight = db.Column(db.Float, default = 1.0)
    dnn_kl_weight = db.Column(db.Float, default = 1.0)
    prediction_log_var_prior = db.Column(db.Float, default = 0.0)
    # do_log = db.Column(db.Boolean, default = False)
    do_chckpt = db.Column(db.Boolean, default = False)
    patience = db.Column(db.Integer, default = 10)
    kl_anneal = db.Column(db.Integer, default = 0)
    w_kl_anneal = db.Column(db.Integer, default = 0)
    dnn_log_var_prior = db.Column(db.Float, default = 0.0)
    log_dir = db.Column(db.String(50), default = 'data/logs')
    model_dir = db.Column(db.String(50), default = 'data/model')
    table_dir = db.Column(db.String(50), default = 'data/tables')
    train_file = db.Column(db.String(50), default = 'MNIST')
    cross_prob = db.Column(db.Float, default = 0.7)
    mutate_prob = db.Column(db.Float, default = 0.01)
    population_size = db.Column(db.Integer, default = 200)
    iterations = db.Column(db.Integer, default = 100)
    # verbose = db.Column(db.Boolean, default = False)
    # make_plots = db.Column(db.Boolean, default = False)
    time_stamp = db.Column(db.Integer, default = 0)
    hostname = db.Column(db.String(50), default = '127.0.0.1')
    num_vae_layers = db.Column(db.Integer, default = 0)
    num_dnn_layers = db.Column(db.Integer, default = 0)
    size_vae_latent = db.Column(db.Integer, default = 0)
    size_vae_hidden = db.Column(db.Integer, default = 0)
    size_dnn_hidden = db.Column(db.Integer, default = 0)
    isTrained = db.Column(db.Integer, default = 0)

