CONTAINER SoftBox
{
    NAME SoftBox;
    INCLUDE Obase;



    GROUP ID_OBJECTPROPERTIES_SB
    {
        DEFAULT 1;

        STRING SB_RENDERER { ANIM OFF; CUSTOMGUI STATICTEXT; WORDWRAP;}

        GROUP{COLUMNS 2; SCALE_H;

            STATICTEXT SB_PE {SCALE_H;}
            BUTTON SB_HELP { SCALE_H;}

        }

        SEPARATOR SB_TARGET{ SCALE_H; }
        SEPARATOR { SCALE_H; }

        GROUP{ SCALE_H;

            SEPARATOR { SCALE_H; }
            BUTTON SB_ADD_TARGET_TAG { SCALE_H;}

        }

        SEPARATOR SB_SOFT_SETTINGS{ SCALE_H; }
        SEPARATOR { SCALE_H; }

        GROUP{ SCALE_H;

            SEPARATOR { SCALE_H; }

            GROUP{COLUMNS 2;

                LONG SB_MODE { CYCLE { SB_SOFTBOX; SB_SPOT;}; SCALE_H; ANIM OFF;}
                BOOL SB_CAST {ANIM OFF;}
            
            }

        }

        GROUP{

            SEPARATOR { SCALE_H; }

            REAL SB_WIDTH {SCALE_H; ANIM OFF; MIN 1.0; MINEX; MAX 100000.0; MAXEX; MINSLIDER 1.0; MAXSLIDER 10000.0; STEP 1.0; UNIT METER; CUSTOMGUI REALSLIDER;}
            REAL SB_HIDTH {SCALE_H; ANIM OFF; MIN 1.0; MINEX; MAX 100000.0; MAXEX; MINSLIDER 1.0; MAXSLIDER 10000.0; STEP 1.0; UNIT METER; CUSTOMGUI REALSLIDER;}
            REAL SB_DIST {SCALE_H; ANIM OFF; MIN 100.0; MINEX; MAX 100000.0; MAXEX; MINSLIDER 100.0; MAXSLIDER 2500.0; STEP 1.0; UNIT METER; CUSTOMGUI REALSLIDER;}

        }

        SEPARATOR SB_LIGHT_SET{ SCALE_H; }
        SEPARATOR { SCALE_H; }

        GROUP{ SCALE_H;

            SEPARATOR { SCALE_H; }

            COLOR SB_LIGHT_COLOR { OPEN; PARENTCOLLAPSE; }

            SEPARATOR { SCALE_H;}

            GROUP{COLUMNS 3; SCALE_H;

            BOOL SB_USED {ANIM OFF;}
            LINK SB_LINK {SCALE_H; ANIM OFF;}
            BOOL SB_INVERT_COLOR {ANIM OFF;}

            }

            SEPARATOR { SCALE_H; }

            REAL SB_BRIGHTNESS {SCALE_H; MIN 0.0; MINEX; MAX 10000.0; MAXEX; MINSLIDER 0.0; MAXSLIDER 200.0; STEP 1.0; UNIT PERCENT; CUSTOMGUI REALSLIDER;}
            
            SEPARATOR { SCALE_H; }

            GROUP{COLUMNS 2;

                BOOL SB_ADDGAIN {ANIM OFF;}
                REAL SB_SAMPLES {SCALE_H; ANIM OFF; MIN 0.0; MINEX; MAX 10000.0; MAXEX; MINSLIDER 0.0; MAXSLIDER 100.0; STEP 1.0; UNIT REAL; CUSTOMGUI REALSLIDER;}

                BOOL SB_USED_BRIGHTNESS_PLANE {ANIM OFF;}
                REAL SB_BRIGHTNESS_PLANE{SCALE_H; MIN 0.0; MINEX; MAX 1000.0; MAXEX; MINSLIDER 0.0; MAXSLIDER 500.0; STEP 1.0; UNIT REAL; CUSTOMGUI REALSLIDER;}

                BOOL SB_SHOW_FALLOFF {ANIM OFF;}

            }


        }

        SEPARATOR SB_SHADOW_SET{ SCALE_H; }
        SEPARATOR { SCALE_H; }

        GROUP{ SCALE_H;

            SEPARATOR { SCALE_H; }

            SEPARATOR { SCALE_H; }

            GROUP {COLUMNS 3; SCALE_H;

                LONG SB_LIGHT_SHADOWTYPE { CYCLE { SB_SH_AREA; SB_SH_NONE; SB_SH_RAY; SB_SH_SOFT;}; ANIM OFF;}

                BOOL SB_LOCK {SCALE_H; ANIM OFF;}
                COLOR SB_SHADOW_COLOR { PARENTCOLLAPSE; ANIM OFF;}

            }

            SEPARATOR { SCALE_H; }

            REAL SB_SHADOW_DENSITY {SCALE_H; MIN 0.0; MINEX; MAX 10000.0; MAXEX; MINSLIDER 0.0; MAXSLIDER 100.0; STEP 1.0; UNIT PERCENT; CUSTOMGUI REALSLIDER;}
            REAL SB_SHADOW_VALUE {SCALE_H; MIN 0.0; MINEX; MAX 10000.0; MAXEX; MINSLIDER 0.0; MAXSLIDER 100.0; STEP 1.0; UNIT PERCENT; CUSTOMGUI REALSLIDER;}

            GROUP {

                SEPARATOR { SCALE_H; }

                REAL SB_LIGHT_SHADOW_DENSITY {SCALE_H; ANIM OFF; MIN 0.0; MINEX; MAX 10000.0; MAXEX; MINSLIDER 0.0; MAXSLIDER 300.0; STEP 1.0; UNIT PERCENT; CUSTOMGUI REALSLIDER;}
                REAL SB_LIGHT_SHADOW_MAXSAMPLES {SCALE_H; ANIM OFF; MIN 0.0; MINEX; MAX 10000.0; MAXEX; MINSLIDER 0.0; MAXSLIDER 500.0; STEP 1.0; UNIT REAL; CUSTOMGUI REALSLIDER;}
                REAL SB_LIGHT_SHADOW_MAPSIZEX {SCALE_H; ANIM OFF; MIN 0.0; MINEX; MAX 10000.0; MAXEX; MINSLIDER 0.0; MAXSLIDER 500.0; STEP 1.0; UNIT REAL; CUSTOMGUI REALSLIDER;}

            }

        }

        SEPARATOR SB_COMPOSITING_SET { SCALE_H; }
        SEPARATOR { SCALE_H; }

        GROUP{

            SEPARATOR { SCALE_H; }

            GROUP { COLUMNS 3; SCALE_H;

                BOOL SB_SB_CAMERA {ANIM OFF;}
                BOOL SB_REFLECTION {ANIM OFF;}
                BOOL SB_SPECULAR {ANIM OFF;}
                BOOL SB_SB_TRANSPARENCY {ANIM OFF;}
                BOOL SB_LIGHT_ON {ANIM OFF;}
                BOOL SB_V_EDITOR {ANIM OFF;}

            }

        }


    }

    GROUP ID_OBJECTPROPERTIES_SB_PRO
    {


        LONG SB_LIGHT_PRO { CYCLE { SB_EXCLUDE; SB_INCLUDE;}; SCALE_H; ANIM OFF;}

        IN_EXCLUDE SB_LIGHT_OBJECT {SCALE_H; OPEN;}


    }


}