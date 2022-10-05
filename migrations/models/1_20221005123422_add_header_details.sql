-- upgrade --
ALTER TABLE "apihit" ADD "response_headers" TEXT;
ALTER TABLE "apihit" ADD "request_headers" TEXT;
-- downgrade --
ALTER TABLE "apihit" DROP COLUMN "response_headers";
ALTER TABLE "apihit" DROP COLUMN "request_headers";
