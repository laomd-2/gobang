#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
using namespace std;

int partition(vector<int>& nums, int first, int last) {
    swap(nums[first], nums[first + rand() % (last - first + 1)]);
    int pivot = nums[first];
    while(first < last) {
        while(first < last && nums[last] >= pivot) {
            last--;
        }
        nums[first] = nums[last];

        while(first < last && nums[first] <= pivot) {
            first++;
        }
        nums[last] = nums[first];
    }
    nums[first] = pivot;
    return first;
}

int quick_select(vector<int> &nums, int k, int i, int j) {
    if (i > j)
        return nums[i];
   	int pivotPos = partition(nums, i, j);
   	int kIdx = i + k - 1;
   	if(kIdx == pivotPos) {
        return nums[pivotPos];
    }
    else if(kIdx < pivotPos) {
        return quick_select(nums, k, i, pivotPos - 1);
    }
    else {
        return quick_select(nums, kIdx - pivotPos, pivotPos + 1, j);
    }
}

int select_kth_smallest(vector<int> v, size_t k) {
    if (k > v.size()) return v[v.size() - 1];
    else if (k < 1) return v[0];
    else return quick_select(v, k, 0, v.size() - 1);
}
int main() {
    srand(time(NULL));
	vector<int> v = {4, 1, 2, 55, 3, 6};
	int k;
	while (cin >> k) {
        cout << select_kth_smallest(v, k) << endl;
	}
	return 0;
}
