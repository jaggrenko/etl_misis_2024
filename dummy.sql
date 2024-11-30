CREATE TABLE public.description_graduates_university (
	object_level varchar(6) NOT NULL,
	object_name varchar(64) NOT NULL,
	gender varchar(7) NOT NULL,
	education_level varchar(64) NOT NULL,
	"year" int2 NOT NULL,
	university text NOT NULL,
	special_section text NOT NULL,
	speciality text NOT NULL,
	speciality_code varchar(8) NOT NULL,
	count_graduate int2 NOT NULL,
	percent_employed real NOT NULL,
	average_salary float4 NULL,
	oktmo varchar(14) NOT NULL,
	okato varchar(9) NOT NULL
);

-- Column comments

COMMENT ON COLUMN public.description_graduates_university.object_name IS 'субъекты федерации';
COMMENT ON COLUMN public.description_graduates_university.gender IS 'пол';
COMMENT ON COLUMN public.description_graduates_university.education_level IS 'образование';
COMMENT ON COLUMN public.description_graduates_university."year" IS 'год';
COMMENT ON COLUMN public.description_graduates_university.university IS 'учебное заведение';
COMMENT ON COLUMN public.description_graduates_university.special_section IS 'направление подготовки';
COMMENT ON COLUMN public.description_graduates_university.speciality IS 'специальность';
COMMENT ON COLUMN public.description_graduates_university.speciality_code IS 'код специальности';
COMMENT ON COLUMN public.description_graduates_university.count_graduate IS 'количество выпускников';
COMMENT ON COLUMN public.description_graduates_university.percent_employed IS 'процент трудоустроенных';
COMMENT ON COLUMN public.description_graduates_university.average_salary IS 'средняя зарплата';
COMMENT ON COLUMN public.description_graduates_university.oktmo IS 'ОКТМО';
COMMENT ON COLUMN public.description_graduates_university.okato IS 'ОКАТО';
