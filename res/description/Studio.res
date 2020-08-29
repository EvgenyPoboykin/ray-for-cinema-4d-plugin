CONTAINER Studio
{
    NAME Studio;
    INCLUDE Obase;


    GROUP ID_OBJECTPROPERTIES_ST
    {

        DEFAULT 1;

        STRING ST_RENDERER { ANIM OFF; CUSTOMGUI STATICTEXT; WORDWRAP;}

        GROUP{COLUMNS 2; SCALE_H;

            STATICTEXT ST_PE {SCALE_H;}
            BUTTON ST_HELP { SCALE_H;}

        }

        SEPARATOR ST_STUDIO_SETTINGS {SCALE_H;}
        SEPARATOR {SCALE_H;}

        GROUP{SCALE_H;
            SEPARATOR {SCALE_H;}
            LONG ST_MODE { CYCLE { ST_C; ST_S; ST_U; ST_L;}; SCALE_H; ANIM OFF;}
        }

        SEPARATOR {SCALE_H;}

        REAL ST_WIDTH {SCALE_H; ANIM OFF; MIN 50.0; MINEX; MAX 100000.0; MAXEX; MINSLIDER 100.0; MAXSLIDER 2500.0; STEP 1.0; UNIT METER; CUSTOMGUI REALSLIDER;}
        REAL ST_HIDTH {SCALE_H; ANIM OFF; MIN 50.0; MINEX; MAX 100000.0; MAXEX; MINSLIDER 100.0; MAXSLIDER 2500.0; STEP 1.0; UNIT METER; CUSTOMGUI REALSLIDER;}
        REAL ST_DEFTH {SCALE_H; ANIM OFF; MIN 50.0; MINEX; MAX 100000.0; MAXEX; MINSLIDER 100.0; MAXSLIDER 2500.0; STEP 1.0; UNIT METER; CUSTOMGUI REALSLIDER;}
        REAL ST_ROUNDING {SCALE_H; ANIM OFF; MIN 1.0; MINEX; MAX 100000.0; MAXEX; MINSLIDER 1.0; MAXSLIDER 200.0; STEP 1.0; UNIT METER; CUSTOMGUI REALSLIDER;}

        SEPARATOR {SCALE_H;}

        GROUP{ COLUMNS 2;
                REAL ST_SUB_VIEWER { ANIM OFF; MIN 1.0; MINEX; MAX 10.0; MAXEX; STEP 1.0; UNIT REAL; }
                REAL ST_SUB_RENDER { ANIM OFF; MIN 1.0; MINEX; MAX 10.0; MAXEX; STEP 1.0; UNIT REAL; }
            }

        SEPARATOR ST_COLOR_SET{ SCALE_H; }
        SEPARATOR {SCALE_H;}

        GROUP{
            SEPARATOR {SCALE_H;}

            LONG ST_RENDER_COLOR { CYCLE { ST_COLOR; ST_REFLECTANCE; }; SCALE_H; ANIM OFF;}
        }

        SEPARATOR {SCALE_H;}

        COLOR ST_STUDIO_COLOR { OPEN; PARENTCOLLAPSE; }



    }

}