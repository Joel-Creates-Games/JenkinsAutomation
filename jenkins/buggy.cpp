#include "buggy.h"

int buggy::GetRandomNumber()
{
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> distrib(1, 10);
    return distrib(gen);
}

std::vector<int>* buggy::MemoryLeakFunction()
{
    std::vector<int>* notDestroyedVector = new std::vector<int>();
    for (size_t i = 0; i < 10; i++)
    {
        notDestroyedVector->push_back(GetRandomNumber());
    }
    return notDestroyedVector;
}
