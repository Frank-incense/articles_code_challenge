import ipdb;
from faker import Faker
from models import Article, Author, Magazine
from db import seed

if __name__ == '__main__':
    seed.seed_data()
    ipdb.set_trace()