-- upgrade --
ALTER TABLE "apihit" ALTER COLUMN "response_headers" TYPE JSONB USING "response_headers"::JSONB;
ALTER TABLE "apihit" ALTER COLUMN "request_headers" TYPE JSONB USING "request_headers"::JSONB;
-- downgrade --
ALTER TABLE "apihit" ALTER COLUMN "response_headers" TYPE TEXT USING "response_headers"::TEXT;
ALTER TABLE "apihit" ALTER COLUMN "request_headers" TYPE TEXT USING "request_headers"::TEXT;
