DROP TABLE IF EXISTS tarefas;

CREATE TABLE tarefas (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    descricao TEXT,
    concluida BOOLEAN DEFAULT FALSE
);

-- Inserindo uma tarefa inicial: "Fazer almoço"
INSERT INTO tarefas (titulo, descricao, concluida)
VALUES ('Fazer almoço', 'Preparar o almoço para o dia.', FALSE);