-- AutoGen Workflow Database Initialization Script
-- This script sets up the initial database structure for the AutoGen application

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create schemas
CREATE SCHEMA IF NOT EXISTS autogen;
CREATE SCHEMA IF NOT EXISTS workflow;
CREATE SCHEMA IF NOT EXISTS analytics;

-- Set search path
SET search_path TO autogen, workflow, analytics, public;

-- Create workflow sessions table
CREATE TABLE IF NOT EXISTS workflow.sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_name VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE,
    config JSONB,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Create workflow tasks table
CREATE TABLE IF NOT EXISTS workflow.tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID REFERENCES workflow.sessions(id) ON DELETE CASCADE,
    task_name VARCHAR(255) NOT NULL,
    task_description TEXT,
    agent_type VARCHAR(100),
    status VARCHAR(50) DEFAULT 'pending',
    input_data JSONB,
    output_data JSONB,
    error_message TEXT,
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create agent interactions table
CREATE TABLE IF NOT EXISTS workflow.agent_interactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    task_id UUID REFERENCES workflow.tasks(id) ON DELETE CASCADE,
    agent_name VARCHAR(100) NOT NULL,
    interaction_type VARCHAR(50), -- 'request', 'response', 'handoff'
    message_content TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create artifacts table
CREATE TABLE IF NOT EXISTS workflow.artifacts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID REFERENCES workflow.sessions(id) ON DELETE CASCADE,
    task_id UUID REFERENCES workflow.tasks(id) ON DELETE CASCADE,
    artifact_type VARCHAR(100), -- 'code', 'document', 'config', 'report'
    artifact_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500),
    content TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create analytics tables
CREATE TABLE IF NOT EXISTS analytics.workflow_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID REFERENCES workflow.sessions(id) ON DELETE CASCADE,
    metric_name VARCHAR(100) NOT NULL,
    metric_value NUMERIC,
    metric_unit VARCHAR(50),
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create API usage tracking
CREATE TABLE IF NOT EXISTS analytics.api_usage (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID REFERENCES workflow.sessions(id) ON DELETE CASCADE,
    api_provider VARCHAR(50), -- 'gemini', 'openai'
    model_name VARCHAR(100),
    tokens_used INTEGER,
    cost_estimate NUMERIC(10,4),
    request_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_sessions_status ON workflow.sessions(status);
CREATE INDEX IF NOT EXISTS idx_sessions_created_at ON workflow.sessions(created_at);
CREATE INDEX IF NOT EXISTS idx_tasks_session_id ON workflow.tasks(session_id);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON workflow.tasks(status);
CREATE INDEX IF NOT EXISTS idx_interactions_task_id ON workflow.agent_interactions(task_id);
CREATE INDEX IF NOT EXISTS idx_artifacts_session_id ON workflow.artifacts(session_id);
CREATE INDEX IF NOT EXISTS idx_metrics_session_id ON analytics.workflow_metrics(session_id);
CREATE INDEX IF NOT EXISTS idx_api_usage_session_id ON analytics.api_usage(session_id);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers
CREATE TRIGGER update_sessions_updated_at 
    BEFORE UPDATE ON workflow.sessions 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert sample data (optional)
INSERT INTO workflow.sessions (session_name, status, config) VALUES 
    ('Sample Workflow', 'completed', '{"model": "gemini-2.0-flash", "temperature": 0.7}'::jsonb)
ON CONFLICT DO NOTHING;

-- Create views for common queries
CREATE OR REPLACE VIEW workflow.session_summary AS
SELECT 
    s.id,
    s.session_name,
    s.status,
    s.created_at,
    s.completed_at,
    COUNT(t.id) as total_tasks,
    COUNT(CASE WHEN t.status = 'completed' THEN 1 END) as completed_tasks,
    COUNT(a.id) as total_artifacts
FROM workflow.sessions s
LEFT JOIN workflow.tasks t ON s.id = t.session_id
LEFT JOIN workflow.artifacts a ON s.id = a.session_id
GROUP BY s.id, s.session_name, s.status, s.created_at, s.completed_at;

-- Grant permissions
GRANT USAGE ON SCHEMA autogen TO autogen_user;
GRANT USAGE ON SCHEMA workflow TO autogen_user;
GRANT USAGE ON SCHEMA analytics TO autogen_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA autogen TO autogen_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA workflow TO autogen_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA analytics TO autogen_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA autogen TO autogen_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA workflow TO autogen_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA analytics TO autogen_user;

-- Create database user for the application (if not exists)
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'autogen_user') THEN
        CREATE ROLE autogen_user LOGIN PASSWORD 'autogen_password';
    END IF;
END
$$;
