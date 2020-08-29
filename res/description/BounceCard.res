CONTAINER BounceCard
{
    NAME BounceCard;
    INCLUDE Obase;


    GROUP ID_OBJECTPROPERTIES_BC
    {

        DEFAULT 1;

        STRING BC_RENDERER { ANIM OFF; CUSTOMGUI STATICTEXT; WORDWRAP;}

        GROUP{COLUMNS 2; SCALE_H;

            STATICTEXT BC_PE {SCALE_H;}
            BUTTON BC_HELP { SCALE_H;}

        }

        SEPARATOR BC_BUTTON_ADDD { SCALE_H; }

        GROUP{

            SEPARATOR { SCALE_H; }
            BUTTON BC_ADD_TARGET_TAG { SCALE_H;}

        }

        SEPARATOR BC_SIZE { SCALE_H; }
        SEPARATOR { SCALE_H; }

        GROUP{

            SEPARATOR { SCALE_H; }

            REAL BC_WIDTH {SCALE_H; ANIM OFF; MIN 1.0; MINEX; MAX 100000.0; MAXEX; MINSLIDER 1.0; MAXSLIDER 5000.0; STEP 1.0; UNIT METER; CUSTOMGUI REALSLIDER;}
            REAL BC_HIDTH {SCALE_H; ANIM OFF; MIN 1.0; MINEX; MAX 100000.0; MAXEX; MINSLIDER 1.0; MAXSLIDER 5000.0; STEP 1.0; UNIT METER; CUSTOMGUI REALSLIDER;}
            REAL BC_RADIUS {SCALE_H; ANIM OFF; MIN 0.0; MINEX; MAX 10000.0; MAXEX; MINSLIDER 0.0; MAXSLIDER 1000.0; STEP 1.0; UNIT METER; CUSTOMGUI REALSLIDER;}

        }

        SEPARATOR BC_COLOR { SCALE_H; }
        SEPARATOR { SCALE_H; }

        GROUP{

            SEPARATOR { SCALE_H; }

            COLOR BC_LIGHT_COLOR { OPEN; PARENTCOLLAPSE; }

            SEPARATOR { SCALE_H; }

            REAL BC_POWER {SCALE_H; MIN 0.0; MINEX; MAX 10000.0; MAXEX; MINSLIDER 0.0; MAXSLIDER 500.0; STEP 1.0; UNIT PERCENT; CUSTOMGUI REALSLIDER;}

            SEPARATOR { SCALE_H; }

            GROUP{COLUMNS 3;

                BOOL BC_USED {ANIM OFF;}
                LINK BC_LINK {SCALE_H; ANIM OFF;}
                BOOL BC_INVERT_COLOR {ANIM OFF;}

            }

        }

        SEPARATOR BC_COMPOSITING_SET { SCALE_H; }
        SEPARATOR { SCALE_H; }

        GROUP{

            SEPARATOR { SCALE_H; }

            GROUP { COLUMNS 3; SCALE_H;

                BOOL BC_SB_CAMERA {ANIM OFF;}
                BOOL BC_SB_TRANSPARENCY {ANIM OFF;}
                BOOL BC_V_EDITOR {ANIM OFF;}

                BOOL BC_LIGHT_RAY {ANIM OFF;}
                BOOL BC_LIGHT_GI {ANIM OFF;}

            }
        }

    }

}