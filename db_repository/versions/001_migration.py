from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
feeds = Table('feeds', pre_meta,
    Column('feed_id', INTEGER, primary_key=True, nullable=False),
    Column('feed_name', VARCHAR(length=128), primary_key=True, nullable=False),
    Column('feed_url', VARCHAR(length=128)),
)

posts = Table('posts', pre_meta,
    Column('post_id', INTEGER, primary_key=True, nullable=False),
    Column('feed_id', INTEGER),
    Column('post_url', VARCHAR(length=128)),
    Column('title', VARCHAR(length=128)),
    Column('content', TEXT),
    Column('create_dataTime', DATETIME),
)

user_feeds = Table('user_feeds', pre_meta,
    Column('users_feeds_id', INTEGER, primary_key=True, nullable=False),
    Column('user_id', INTEGER),
    Column('feed_id', INTEGER),
    Column('feed_name', VARCHAR(length=128)),
)

user_posts = Table('user_posts', pre_meta,
    Column('users_posts_id', INTEGER, primary_key=True, nullable=False),
    Column('user_id', INTEGER),
    Column('news_id', INTEGER),
)

users = Table('users', pre_meta,
    Column('user_id', INTEGER, primary_key=True, nullable=False),
    Column('password_hash', VARCHAR(length=128)),
    Column('login', VARCHAR(length=32)),
    Column('email', VARCHAR(length=64)),
    Column('name', VARCHAR(length=16)),
    Column('surname', VARCHAR(length=16)),
)

post = Table('post', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('title', String(length=140)),
    Column('text', String(length=140)),
    Column('timestamp', DateTime),
    Column('user_id', Integer),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('password_hash', String(length=128)),
    Column('login', String(length=32)),
    Column('email', String(length=64)),
    Column('name', String(length=16)),
    Column('surname', String(length=16)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['feeds'].drop()
    pre_meta.tables['posts'].drop()
    pre_meta.tables['user_feeds'].drop()
    pre_meta.tables['user_posts'].drop()
    pre_meta.tables['users'].drop()
    post_meta.tables['post'].create()
    post_meta.tables['user'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['feeds'].create()
    pre_meta.tables['posts'].create()
    pre_meta.tables['user_feeds'].create()
    pre_meta.tables['user_posts'].create()
    pre_meta.tables['users'].create()
    post_meta.tables['post'].drop()
    post_meta.tables['user'].drop()
