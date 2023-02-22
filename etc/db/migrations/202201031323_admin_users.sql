--migrate:up


CREATE TABLE admin_users (
    user_id INTEGER,
    en BOOLEAN,
    ctime TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT (now() at time zone 'utc'),
    atime TIMESTAMP WITHOUT TIME ZONE DEFAULT NULL,
    dtime TIMESTAMP WITHOUT TIME ZONE DEFAULT NULL
);

CREATE INDEX admin_users_user_id_en ON admin_users (user_id, en);
ALTER TABLE admin_users
    ADD CONSTRAINT admin_users_user_id_fkey FOREIGN KEY (user_id)
    REFERENCES users(id)
    ON DELETE CASCADE;


--migrate:down


DROP TABLE admin_users;