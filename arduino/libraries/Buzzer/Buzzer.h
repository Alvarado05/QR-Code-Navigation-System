#ifndef Buzzer_h
#define Buzzer_h

class Buzzer
{
    public:
    //Constructors
    Buzzer(byte buzzerPin);

    //Functions
    void arrived();
    void rotate();
    void error();

};

#endif