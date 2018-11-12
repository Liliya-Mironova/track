CREATE TABLE users (
	user_id SERIAL PRIMARY KEY,
	name TEXT NOT NULL
	CHECK (length(name) < 32),
	nick TEXT NOT NULL UNIQUE
	CHECK (length(name) < 32),
	avatar TEXT
);

create table chats (
	chat_id serial primary key,
	is_group_chat boolean,
	topic text not null
	CHECK (length(topic) < 256),
	last_message text
);

create table messages (
	message_id serial primary key,
	chat_id integer not null
	references chats(chat_id),
	user_id integer not null
	references users(user_id),
	content text not null
	check (length(content) < 65536),
	added_at timestamp not null default now() 
);

create table members (
	member_id serial primary key,
	user_id integer not null
	references users(user_id),
	chat_id integer not null
	references chats(chat_id),
	new_messages integer,
	last_read_message_id integer
	references messages(message_id)
);

create table attachments (
	attach_id serial primary key,
	chat_id integer not null
	references chats(chat_id),
	user_id integer not null
	references users(user_id),
	message_id integer not null
	references messages(message_id),
	type text not null
	CHECK (length(type) < 256)
);


insert into users (name, nick)
values ('lmironov', 'LiliyaMironova'),
	   ('kakimov', 'KirillAkimov'),
	   ('alavrentev', 'KirillLavrentev'),
	   ('ngaiduchenko', 'NickolasGaiduchenko'),
	   ('demtsev', 'DaniilEmtsev'),
	   ('dpetrov', 'DaryaPetrova'),
	   ('tbabushkina', 'TatyanaBabushkina');

insert into chats (is_group_chat, topic)
values (false, 'dialogkl'),
	   (false, 'dialogkk')
	   (false, 'dialogld');

insert into messages (chat_id, user_id, content)
values (1, 1, 'Hello, Kirill!'),
	   (1, 2, 'Hello, Lily!'),
	   (2, 2, 'Hi, Kir'),
	   (2, 3, 'Hi too');

insert into members (chat_id, user_id)
values (1, 1),
	   (1, 2),
	   (2, 2),
	   (2, 3),
	   (3, 1),
	   (3, 4);
