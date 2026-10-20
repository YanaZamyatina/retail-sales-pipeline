create table if not exists sales(
    id serial primary key,
    created_at TIMESTAMP not null,
    doc_id INT not null,
    shop_id INT not null,
    cash_desk_id INT not null,
    category VARCHAR(100) not null,
    item VARCHAR(100) not null,
    amount INT not null,
    price NUMERIC(10, 2) not null,
    discount NUMERIC(10, 2) DEFAULT 0.00
)