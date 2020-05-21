#ifndef Buzzer_h
#define Buzzer_h

#include <Arduino.h>

class Buzzer
{
    public:
    //Constructors
    Buzzer(byte buzzerPin);

    //Functions
    void arrived();
    void rotate();
    void error();

    private:
        byte _buzzerPin;

};

#endif