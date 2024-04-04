#include <iostream>
#include <map>
#include <array>
#include <list>
#include <optional>
#include <stdlib.h>
#include <nlohmann/json.hpp>
#include <boost/core/demangle.hpp>

using json = nlohmann::json;
using boost::core::demangle;
using namespace std;

enum Weekday {
	MONDAY = 1,
	TUESDAY = 2,
	WEDNESDAY = 3,
	THURSDAY = 4,
	FRIDAY = 5,
	SATURDAY = 6,
	SUNDAY = 7,
};

struct Wrapper {
	string src;
	string dest;
	int prio;
	Weekday weekday;
	map<string, int> m;
	float f;
	bool b;
	int ttl;

	json toJson() {
		json j;
		j[0] = src;
		j[1] = dest;
		j[2] = prio;
		j[4] = m;
		j[5] = f;
		j[6] = b;
		j[7] = ttl;
		return j;
	}

	vector<uint8_t> serialize() {
		return json::to_cbor(toJson());
	}

	void fromJson(json j) {
		src = j[0];
		dest = j[1];
		prio = j[2];
		m = j[4];
		f = j[5];
		b = j[6];
		ttl = j[7];
	}

	void deserialize(vector<uint8_t> ourCbor) {
		fromJson(json::from_cbor(ourCbor));
	}

};

struct MyClass {
	Wrapper v;
	map<string, vector<float>> w;
	array<int, 10> x;
	map<string, vector<map<string, int>>> y;
	map<string, map<int, vector<string>>> z;

	json toJson() {
		json j;
		j[0] = v.toJson();
		j[1] = w;
		j[2] = x;
		j[3] = y;
		j[4] = z;
		return j;
	}

	vector<uint8_t> serialize() {
		return json::to_cbor(toJson());
	}

	void fromJson(json j) {
		v.fromJson(j[0]);
		w = j[1];
		x = j[2];
		y = j[3];
		z = j[4];
	}

	void deserialize(vector<uint8_t> ourCbor) {
		fromJson(json::from_cbor(ourCbor));
	}

};

