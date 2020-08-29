CONTAINER GlobalLight
{
    NAME GlobalLight;
    INCLUDE Obase;



    GROUP ID_OBJECTPROPERTIES_GL
    {

        DEFAULT 1;

        STRING GL_RENDERER { ANIM OFF; CUSTOMGUI STATICTEXT; WORDWRAP;}

        GROUP{COLUMNS 2; SCALE_H;

            STATICTEXT GL_PE {SCALE_H;}
            BUTTON GL_HELP { SCALE_H;}

        }

        SEPARATOR GL_LIGHT_SET{ SCALE_H;}
        SEPARATOR { SCALE_H;}

        GROUP{
            SEPARATOR { SCALE_H;}
            COLOR GL_LIGHT_COLOR { OPEN; PARENTCOLLAPSE; }
        }

        SEPARATOR { SCALE_H;}

        REAL GL_LIGHT_STR {SCALE_H; MIN 0.0; MINEX; MAX 10000.0; MAXEX; MINSLIDER 0.0; MAXSLIDER 100.0; STEP 1.0; UNIT PERCENT; CUSTOMGUI REALSLIDER;}

        SEPARATOR GL_USED_REFERENCE{ SCALE_H;}
        SEPARATOR { SCALE_H;}

        GROUP{COLUMNS 3;

            BOOL GL_USED {ANIM OFF;}
            LINK GL_LINK {SCALE_H; ANIM OFF;}
            BOOL GL_INVERT_COLOR {ANIM OFF;}

            }


    }


}