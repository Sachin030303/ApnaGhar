--
-- PostgreSQL database dump
--

\restrict nQj9VubAuLdEHLSbQ8D2wXpGqaTr9Zx2sgThx1Pq0aYxhg6rpIU8DJcR47AW8Xv

-- Dumped from database version 18.6
-- Dumped by pg_dump version 18.6

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

--
-- Name: furnishingstatus; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.furnishingstatus AS ENUM (
    'FURNISHED',
    'SEMI_FURNISHED',
    'UNFURNISHED'
);


ALTER TYPE public.furnishingstatus OWNER TO postgres;

--
-- Name: propertytype; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.propertytype AS ENUM (
    'APARTMENT',
    'HOUSE',
    'VILLA',
    'PG',
    'HOSTEL',
    'ROOM'
);


ALTER TYPE public.propertytype OWNER TO postgres;

--
-- Name: userrole; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.userrole AS ENUM (
    'STUDENT',
    'PROFESSIONAL',
    'OWNER',
    'ADMIN'
);


ALTER TYPE public.userrole OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: properties; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.properties (
    id integer NOT NULL,
    owner_id integer NOT NULL,
    title character varying(200) NOT NULL,
    description text,
    property_type public.propertytype NOT NULL,
    address character varying(500) NOT NULL,
    city character varying(100) NOT NULL,
    state character varying(100) NOT NULL,
    pincode character varying(10) NOT NULL,
    latitude double precision,
    longitude double precision,
    monthly_rent double precision NOT NULL,
    security_deposit double precision,
    bedrooms integer,
    bathrooms integer,
    furnishing_status public.furnishingstatus,
    available_from timestamp without time zone,
    is_available boolean NOT NULL,
    is_verified boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.properties OWNER TO postgres;

--
-- Name: properties_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.properties_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.properties_id_seq OWNER TO postgres;

--
-- Name: properties_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.properties_id_seq OWNED BY public.properties.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    email character varying(255) NOT NULL,
    password_hash character varying(255) NOT NULL,
    full_name character varying(100) NOT NULL,
    role public.userrole NOT NULL,
    is_active boolean NOT NULL,
    is_verified boolean NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: properties id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.properties ALTER COLUMN id SET DEFAULT nextval('public.properties_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
9ed785a80c8f
\.


--
-- Data for Name: properties; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.properties (id, owner_id, title, description, property_type, address, city, state, pincode, latitude, longitude, monthly_rent, security_deposit, bedrooms, bathrooms, furnishing_status, available_from, is_available, is_verified, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, email, password_hash, full_name, role, is_active, is_verified, created_at, updated_at) FROM stdin;
1	test.owner@apnaghar.com	temporary-test-hash	Test Owner	OWNER	t	t	2026-09-28 02:23:44.319596	2026-09-28 02:23:44.319596
2	sachin.test@apnaghar.com	$2b$12$Htk2aMG7qlYUZGG8iR1P0OieKrzrdszvuo35GgMZ/qXZSid//KYUW	Sachin Test	OWNER	t	f	2026-09-30 19:15:03.96684	2026-09-30 19:15:03.966846
3	shreshth@example.com	$2b$12$lKYgrU1cRkHHWB5y6uXtfOC3kPkEtkx5IemAw0GxcyAbvXukfWHnq	shreshth	STUDENT	t	f	2026-09-30 21:14:16.200187	2026-09-30 21:14:16.200195
4	shreshth1@example.com	$2b$12$XYOYkhqfGLBDkLQCVv4wieU7BHk9uGmvJAq8rrIfUAovfxhusR/US	shreshth	OWNER	t	f	2026-09-30 21:15:26.593253	2026-09-30 21:15:26.593258
\.


--
-- Name: properties_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.properties_id_seq', 3, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 4, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: properties properties_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.properties
    ADD CONSTRAINT properties_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_properties_city; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_properties_city ON public.properties USING btree (city);


--
-- Name: ix_properties_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_properties_id ON public.properties USING btree (id);


--
-- Name: ix_properties_owner_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_properties_owner_id ON public.properties USING btree (owner_id);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- Name: properties properties_owner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.properties
    ADD CONSTRAINT properties_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict nQj9VubAuLdEHLSbQ8D2wXpGqaTr9Zx2sgThx1Pq0aYxhg6rpIU8DJcR47AW8Xv

