CREATE TABLE virtual_machines (
    id SERIAL PRIMARY KEY,
    ram_amount BIGINT NOT NULL,
    cpu_amount INT NOT NULL,
    is_online BOOLEAN DEFAULT TRUE,
    is_auth BOOLEAN DEFAULT TRUE
);

CREATE TABLE hard_drives (
    id SERIAL PRIMARY KEY,
    vm_id INT REFERENCES virtual_machines(id),
    rom_amount BIGINT NOT NULL
);