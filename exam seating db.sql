--
-- PostgreSQL database dump
--

-- Dumped from database version 17.2
-- Dumped by pg_dump version 17.2

-- Started on 2025-03-12 18:51:25

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
-- TOC entry 4900 (class 1262 OID 16860)
-- Name: exam seating; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE "exam seating" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_India.1252';


ALTER DATABASE "exam seating" OWNER TO postgres;

\connect -reuse-previous=on "dbname='exam seating'"

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
-- TOC entry 222 (class 1259 OID 16881)
-- Name: exams; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.exams (
    id integer NOT NULL,
    exam_name character varying(100) NOT NULL,
    exam_date date NOT NULL
);


ALTER TABLE public.exams OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16880)
-- Name: exams_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.exams_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.exams_id_seq OWNER TO postgres;

--
-- TOC entry 4901 (class 0 OID 0)
-- Dependencies: 221
-- Name: exams_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.exams_id_seq OWNED BY public.exams.id;


--
-- TOC entry 224 (class 1259 OID 16888)
-- Name: rooms; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rooms (
    id integer NOT NULL,
    room_name character varying(50) NOT NULL,
    capacity integer NOT NULL
);


ALTER TABLE public.rooms OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16887)
-- Name: rooms_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.rooms_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.rooms_id_seq OWNER TO postgres;

--
-- TOC entry 4902 (class 0 OID 0)
-- Dependencies: 223
-- Name: rooms_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.rooms_id_seq OWNED BY public.rooms.id;


--
-- TOC entry 226 (class 1259 OID 16897)
-- Name: seating_arrangement; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.seating_arrangement (
    id integer NOT NULL,
    student_id integer,
    exam_id integer,
    room_id integer,
    seat_number integer NOT NULL
);


ALTER TABLE public.seating_arrangement OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 16896)
-- Name: seating_arrangement_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.seating_arrangement_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.seating_arrangement_id_seq OWNER TO postgres;

--
-- TOC entry 4903 (class 0 OID 0)
-- Dependencies: 225
-- Name: seating_arrangement_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.seating_arrangement_id_seq OWNED BY public.seating_arrangement.id;


--
-- TOC entry 220 (class 1259 OID 16872)
-- Name: students; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.students (
    id integer NOT NULL,
    roll_number character varying(20) NOT NULL,
    name character varying(100) NOT NULL
);


ALTER TABLE public.students OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16871)
-- Name: students_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.students_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.students_id_seq OWNER TO postgres;

--
-- TOC entry 4904 (class 0 OID 0)
-- Dependencies: 219
-- Name: students_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.students_id_seq OWNED BY public.students.id;


--
-- TOC entry 218 (class 1259 OID 16862)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(50) NOT NULL,
    password character varying(50) NOT NULL,
    role character varying(10) NOT NULL,
    CONSTRAINT users_role_check CHECK (((role)::text = ANY ((ARRAY['admin'::character varying, 'student'::character varying])::text[])))
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16861)
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
-- TOC entry 4905 (class 0 OID 0)
-- Dependencies: 217
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 4717 (class 2604 OID 16884)
-- Name: exams id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exams ALTER COLUMN id SET DEFAULT nextval('public.exams_id_seq'::regclass);


--
-- TOC entry 4718 (class 2604 OID 16891)
-- Name: rooms id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms ALTER COLUMN id SET DEFAULT nextval('public.rooms_id_seq'::regclass);


--
-- TOC entry 4719 (class 2604 OID 16900)
-- Name: seating_arrangement id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.seating_arrangement ALTER COLUMN id SET DEFAULT nextval('public.seating_arrangement_id_seq'::regclass);


--
-- TOC entry 4716 (class 2604 OID 16875)
-- Name: students id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.students ALTER COLUMN id SET DEFAULT nextval('public.students_id_seq'::regclass);


--
-- TOC entry 4715 (class 2604 OID 16865)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 4890 (class 0 OID 16881)
-- Dependencies: 222
-- Data for Name: exams; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.exams (id, exam_name, exam_date) FROM stdin;
1	CR	2025-04-04
2	WSN	2025-04-06
4	DSP	2025-04-09
5	VLSI	2025-04-11
6	DSA	2025-04-15
8	C fundamentals	2025-04-13
7	ED	2025-04-18
9	SQL	2025-04-25
\.


--
-- TOC entry 4892 (class 0 OID 16888)
-- Dependencies: 224
-- Data for Name: rooms; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rooms (id, room_name, capacity) FROM stdin;
5	A2	20
7	A5	30
6	A3	20
1	A4	15
8	A7	30
2	A6	10
4	A1	15
\.


--
-- TOC entry 4894 (class 0 OID 16897)
-- Dependencies: 226
-- Data for Name: seating_arrangement; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.seating_arrangement (id, student_id, exam_id, room_id, seat_number) FROM stdin;
1252	2	1	4	1
1253	7	1	4	2
1254	4	1	4	3
1255	10	1	4	4
1256	1	1	4	5
1257	14	1	4	6
1258	12	1	4	7
1259	11	1	4	8
1260	6	1	4	9
1261	3	1	4	10
1262	5	1	4	11
1263	25	1	4	12
1264	20	1	4	13
1265	21	1	4	14
1266	8	1	4	15
1267	16	1	5	1
1268	17	1	5	2
1269	22	1	5	3
1270	23	1	5	4
1271	19	1	5	5
1272	18	1	5	6
1273	27	1	5	7
1274	26	1	5	8
1275	24	1	5	9
1276	28	1	5	10
1302	2	4	4	1
1303	7	4	4	2
1304	4	4	4	3
1305	10	4	4	4
1306	1	4	4	5
1307	14	4	4	6
1308	12	4	4	7
1309	11	4	4	8
1310	6	4	4	9
1311	3	4	4	10
1312	5	4	4	11
1313	25	4	4	12
1314	20	4	4	13
1315	21	4	4	14
1316	8	4	4	15
1317	16	4	5	1
1318	17	4	5	2
1319	22	4	5	3
1320	23	4	5	4
1321	19	4	5	5
1322	18	4	5	6
1323	27	4	5	7
1324	26	4	5	8
1325	24	4	5	9
1326	28	4	5	10
1352	2	6	4	1
1353	7	6	4	2
1354	4	6	4	3
1355	10	6	4	4
1356	1	6	4	5
1357	14	6	4	6
1358	12	6	4	7
1359	11	6	4	8
1360	6	6	4	9
1361	3	6	4	10
1362	5	6	4	11
1363	25	6	4	12
1364	20	6	4	13
1365	21	6	4	14
1366	8	6	4	15
1367	16	6	5	1
1368	17	6	5	2
1369	22	6	5	3
1370	23	6	5	4
1371	19	6	5	5
1372	18	6	5	6
1373	27	6	5	7
1374	26	6	5	8
1375	24	6	5	9
1376	28	6	5	10
1402	2	7	4	1
1403	7	7	4	2
1404	4	7	4	3
1405	10	7	4	4
1406	1	7	4	5
1407	14	7	4	6
1408	12	7	4	7
1409	11	7	4	8
1410	6	7	4	9
1411	3	7	4	10
1412	5	7	4	11
1413	25	7	4	12
1414	20	7	4	13
1415	21	7	4	14
1416	8	7	4	15
1417	16	7	5	1
1418	17	7	5	2
1419	22	7	5	3
1420	23	7	5	4
1421	19	7	5	5
1422	18	7	5	6
1423	27	7	5	7
1424	26	7	5	8
1425	24	7	5	9
1426	28	7	5	10
1277	2	2	4	1
1278	7	2	4	2
1279	4	2	4	3
1280	10	2	4	4
1281	1	2	4	5
1282	14	2	4	6
1283	12	2	4	7
1284	11	2	4	8
1285	6	2	4	9
1286	3	2	4	10
1287	5	2	4	11
1288	25	2	4	12
1289	20	2	4	13
1290	21	2	4	14
1291	8	2	4	15
1292	16	2	5	1
1293	17	2	5	2
1294	22	2	5	3
1295	23	2	5	4
1296	19	2	5	5
1297	18	2	5	6
1298	27	2	5	7
1299	26	2	5	8
1300	24	2	5	9
1301	28	2	5	10
1327	2	5	4	1
1328	7	5	4	2
1329	4	5	4	3
1330	10	5	4	4
1331	1	5	4	5
1332	14	5	4	6
1333	12	5	4	7
1334	11	5	4	8
1335	6	5	4	9
1336	3	5	4	10
1337	5	5	4	11
1338	25	5	4	12
1339	20	5	4	13
1340	21	5	4	14
1341	8	5	4	15
1342	16	5	5	1
1343	17	5	5	2
1344	22	5	5	3
1345	23	5	5	4
1346	19	5	5	5
1347	18	5	5	6
1348	27	5	5	7
1349	26	5	5	8
1350	24	5	5	9
1351	28	5	5	10
1377	2	8	4	1
1378	7	8	4	2
1379	4	8	4	3
1380	10	8	4	4
1381	1	8	4	5
1382	14	8	4	6
1383	12	8	4	7
1384	11	8	4	8
1385	6	8	4	9
1386	3	8	4	10
1387	5	8	4	11
1388	25	8	4	12
1389	20	8	4	13
1390	21	8	4	14
1391	8	8	4	15
1392	16	8	5	1
1508	2	9	4	1
1509	7	9	4	2
1510	4	9	4	3
1511	10	9	4	4
1512	1	9	4	5
1513	32	9	4	6
1514	14	9	4	7
1515	12	9	4	8
1516	31	9	4	9
1517	11	9	4	10
1518	6	9	4	11
1519	30	9	4	12
1520	3	9	4	13
1521	5	9	4	14
1522	25	9	4	15
1523	20	9	5	1
1524	21	9	5	2
1525	8	9	5	3
1526	16	9	5	4
1527	17	9	5	5
1528	22	9	5	6
1529	23	9	5	7
1530	19	9	5	8
1531	18	9	5	9
1532	27	9	5	10
1533	26	9	5	11
1534	24	9	5	12
1535	28	9	5	13
1536	29	9	5	14
1393	17	8	5	2
1394	22	8	5	3
1395	23	8	5	4
1396	19	8	5	5
1397	18	8	5	6
1398	27	8	5	7
1399	26	8	5	8
1400	24	8	5	9
1401	28	8	5	10
\.


--
-- TOC entry 4888 (class 0 OID 16872)
-- Dependencies: 220
-- Data for Name: students; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.students (id, roll_number, name) FROM stdin;
3	24	karthega
4	5	akila
5	25	Roopa
6	22	Murali
11	20	Raji
12	15	Mohana
14	12	durga
16	40	sharmila
17	42	subiksha
18	50	yuvashree
19	49	vani
20	30	nandhini
2	1	abinaya
10	7	Akshaya
21	32	Mohan
22	47	Vijay
23	48	roshini
24	56	Shobi
25	28	keerthi
1	10	Darani
26	55	Uthra
8	38	Swetha
27	52	Priya
28	57	Ramya
29	60	yamini
7	2	Angel
30	23	nisha
31	19	raj
32	11	deepa
\.


--
-- TOC entry 4886 (class 0 OID 16862)
-- Dependencies: 218
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, password, role) FROM stdin;
1	admin	admin123	admin
2	student	123	student
\.


--
-- TOC entry 4906 (class 0 OID 0)
-- Dependencies: 221
-- Name: exams_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.exams_id_seq', 9, true);


--
-- TOC entry 4907 (class 0 OID 0)
-- Dependencies: 223
-- Name: rooms_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rooms_id_seq', 8, true);


--
-- TOC entry 4908 (class 0 OID 0)
-- Dependencies: 225
-- Name: seating_arrangement_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.seating_arrangement_id_seq', 1536, true);


--
-- TOC entry 4909 (class 0 OID 0)
-- Dependencies: 219
-- Name: students_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.students_id_seq', 32, true);


--
-- TOC entry 4910 (class 0 OID 0)
-- Dependencies: 217
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 2, true);


--
-- TOC entry 4730 (class 2606 OID 16886)
-- Name: exams exams_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.exams
    ADD CONSTRAINT exams_pkey PRIMARY KEY (id);


--
-- TOC entry 4732 (class 2606 OID 16893)
-- Name: rooms rooms_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms
    ADD CONSTRAINT rooms_pkey PRIMARY KEY (id);


--
-- TOC entry 4734 (class 2606 OID 16895)
-- Name: rooms rooms_room_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rooms
    ADD CONSTRAINT rooms_room_name_key UNIQUE (room_name);


--
-- TOC entry 4736 (class 2606 OID 16902)
-- Name: seating_arrangement seating_arrangement_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.seating_arrangement
    ADD CONSTRAINT seating_arrangement_pkey PRIMARY KEY (id);


--
-- TOC entry 4726 (class 2606 OID 16877)
-- Name: students students_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.students
    ADD CONSTRAINT students_pkey PRIMARY KEY (id);


--
-- TOC entry 4728 (class 2606 OID 16879)
-- Name: students students_roll_number_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.students
    ADD CONSTRAINT students_roll_number_key UNIQUE (roll_number);


--
-- TOC entry 4722 (class 2606 OID 16868)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 4724 (class 2606 OID 16870)
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- TOC entry 4737 (class 2606 OID 16908)
-- Name: seating_arrangement seating_arrangement_exam_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.seating_arrangement
    ADD CONSTRAINT seating_arrangement_exam_id_fkey FOREIGN KEY (exam_id) REFERENCES public.exams(id) ON DELETE CASCADE;


--
-- TOC entry 4738 (class 2606 OID 16913)
-- Name: seating_arrangement seating_arrangement_room_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.seating_arrangement
    ADD CONSTRAINT seating_arrangement_room_id_fkey FOREIGN KEY (room_id) REFERENCES public.rooms(id) ON DELETE CASCADE;


--
-- TOC entry 4739 (class 2606 OID 16903)
-- Name: seating_arrangement seating_arrangement_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.seating_arrangement
    ADD CONSTRAINT seating_arrangement_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.students(id) ON DELETE CASCADE;


-- Completed on 2025-03-12 18:51:25

--
-- PostgreSQL database dump complete
--

