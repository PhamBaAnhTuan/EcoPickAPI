CREATE TABLE "event_eventparticipants" ("id" uuid NOT NULL PRIMARY KEY, "status" varchar(50) NOT NULL, "joined_at" timestamp with time zone NOT NULL, "checked_in_at" timestamp with time zone NULL, "event_id" uuid NULL, "user_id" uuid NULL);
ALTER TABLE "event_eventparticipants" ADD CONSTRAINT "event_eventparticipants_event_id_user_id_f19f6be3_uniq" UNIQUE ("event_id", "user_id");
ALTER TABLE "event_eventparticipants" ADD CONSTRAINT "event_eventparticipants_event_id_7c16497d_fk_event_event_id" FOREIGN KEY ("event_id") REFERENCES "event_event" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "event_eventparticipants" ADD CONSTRAINT "event_eventparticipants_user_id_349821a9_fk_oauth_user_id" FOREIGN KEY ("user_id") REFERENCES "oauth_user" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "event_eventparticipants_event_id_7c16497d" ON "event_eventparticipants" ("event_id");
CREATE INDEX "event_eventparticipants_user_id_349821a9" ON "event_eventparticipants" ("user_id");
