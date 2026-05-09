\restrict dbmate

-- Dumped from database version 16.13
-- Dumped by pg_dump version 17.9 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: geeknews_fetch_runs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.geeknews_fetch_runs (
    id bigint NOT NULL,
    source_name text NOT NULL,
    status text NOT NULL,
    fetched_at timestamp with time zone DEFAULT now() NOT NULL,
    item_count integer DEFAULT 0 NOT NULL,
    error_message text,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT geeknews_fetch_runs_status_check CHECK ((status = ANY (ARRAY['success'::text, 'failure'::text])))
);


--
-- Name: geeknews_fetch_runs_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.geeknews_fetch_runs ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.geeknews_fetch_runs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: geeknews_items; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.geeknews_items (
    id bigint NOT NULL,
    fetch_run_id bigint,
    source_name text NOT NULL,
    external_id text NOT NULL,
    title text NOT NULL,
    source_url text NOT NULL,
    published_at timestamp with time zone,
    fetched_at timestamp with time zone DEFAULT now() NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: geeknews_items_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.geeknews_items ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.geeknews_items_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: schema_migrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.schema_migrations (
    version character varying NOT NULL
);


--
-- Name: geeknews_fetch_runs geeknews_fetch_runs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.geeknews_fetch_runs
    ADD CONSTRAINT geeknews_fetch_runs_pkey PRIMARY KEY (id);


--
-- Name: geeknews_items geeknews_items_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.geeknews_items
    ADD CONSTRAINT geeknews_items_pkey PRIMARY KEY (id);


--
-- Name: geeknews_items geeknews_items_source_external_id_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.geeknews_items
    ADD CONSTRAINT geeknews_items_source_external_id_unique UNIQUE (source_name, external_id);


--
-- Name: schema_migrations schema_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.schema_migrations
    ADD CONSTRAINT schema_migrations_pkey PRIMARY KEY (version);


--
-- Name: geeknews_fetch_runs_source_fetched_at_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX geeknews_fetch_runs_source_fetched_at_idx ON public.geeknews_fetch_runs USING btree (source_name, fetched_at DESC);


--
-- Name: geeknews_items_fetched_at_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX geeknews_items_fetched_at_idx ON public.geeknews_items USING btree (fetched_at DESC, id DESC);


--
-- Name: geeknews_items_published_at_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX geeknews_items_published_at_idx ON public.geeknews_items USING btree (published_at DESC NULLS LAST, id DESC);


--
-- Name: geeknews_items geeknews_items_fetch_run_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.geeknews_items
    ADD CONSTRAINT geeknews_items_fetch_run_id_fkey FOREIGN KEY (fetch_run_id) REFERENCES public.geeknews_fetch_runs(id) ON DELETE SET NULL;


--
-- PostgreSQL database dump complete
--

\unrestrict dbmate


--
-- Dbmate schema migrations
--

INSERT INTO public.schema_migrations (version) VALUES
    ('20260509000000');
