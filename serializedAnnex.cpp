#include <iostream>
#include <map>
#include <array>
#include <list>
#include <stdlib.h>

#include "generated.h"

using namespace std;

int main(int argc, char *argv[])
{
    Wrapper cls1;
    cls1.src = "Its";
	cls1.dest = "so";
	cls1.prio = 73;
	cls1.m = {{"CPU", 10}, {"GPU", 15}, {"RAM", 20}};
	cls1.f = 3.14;
	cls1.b = false;
	cls1.ttl = -46;

    MyClass cls2;
    cls2.v = cls1;
	cls2.w = {{"CPU", {2.0, 5.2}}, {"GPU", {2.0, 5.2}}, {"RAM", {2.0, 5.2}}};
	cls2.x = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
	cls2.y = {{"CPU", {{{"CPU", 10}, {"GPU", 15}, {"RAM", 20}}, {{"CPU", 10}, {"GPU", 15}, {"RAM", 20}}}}, {"GPU", {{{"CPU", 10}, {"GPU", 15}, {"RAM", 20}}, {{"CPU", 10}, {"GPU", 15}, {"RAM", 20}}}}, {"RAM", {{{"CPU", 10}, {"GPU", 15}, {"RAM", 20}}, {{"CPU", 10}, {"GPU", 15}, {"RAM", 20}}}}};
	cls2.z = {{"CPU", {{10, {"Hi", "Hello"}}, {15, {"Hi", "Hello"}}, {20, {"Hi", "Hello"}}}}, {"GPU", {{10, {"Hi", "Hello"}}, {15, {"Hi", "Hello"}}, {20, {"Hi", "Hello"}}}}};

    auto cb = cls2.serialize();
	cout << demangle(typeid(cb).name()) << endl;
    for (auto c : cb) {
        cout << ' ' << int(c);
    }
    cout << endl << "cbor message is " << size(cb) << " bytes" << endl << endl;
	cls2.deserialize(cb);
	cout << cls2.v.ttl << endl;
}