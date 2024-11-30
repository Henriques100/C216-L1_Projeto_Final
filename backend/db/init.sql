DROP TABLE IF EXISTS tarefas;

CREATE TABLE tarefas (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    descricao TEXT,
    concluida BOOLEAN DEFAULT FALSE,
    prazo VARCHAR(255),
    diario BOOLEAN DEFAULT FALSE
);

-- Inserindo uma tarefa inicial: "Fazer almoço"
INSERT INTO tarefas (titulo, descricao, concluida, prazo, diario)
VALUES (
    'Fazer almoço', 
    'Preparar o almoço para o dia.', 
    FALSE, 
    '12:00:00',
    TRUE
);
