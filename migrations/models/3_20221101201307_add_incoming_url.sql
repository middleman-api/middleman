-- upgrade --
ALTER TABLE "site" ADD "incoming_url" VARCHAR(253) NOT NULL;
-- downgrade --
ALTER TABLE "site" DROP COLUMN "incoming_url";
