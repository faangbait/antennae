package main

import (
	"reflect"
	"testing"
)

func main() {
	twoSum([]int{3,2,4}, 6)
}

func twoSum(nums []int, target int) []int {
	hashmap := make(map[int]int)

	for i := 0; i < len(nums); i++ {
		conumber := target - nums[i]
		// fmt.Println("Conumber for ", nums[i], " is ", target-nums[i])
		index, ok := hashmap[conumber]
		if ok {
			// fmt.Println("Found ", index, i)
			return []int{index, i}
		} else {
			hashmap[nums[i]] = i
		}
	}
	return []int{}
}

func Test_twoSum(t *testing.T) {
	type args struct {
		nums   []int
		target int
	}
	tests := []struct {
		name string
		args args
		want []int
	}{
		{
			name: "test1",
			args: args{
				nums:   []int{2,7,11,15},
				target: 9,
			},
			want: []int{0,1},
		},
		{
			name: "test2",
			args: args{
				nums:   []int{3,2,4},
				target: 6,
			},
			want: []int{1,2},
		},
		{
			name: "test3",
			args: args{
				nums:   []int{3,3},
				target: 6,
			},
			want: []int{0,1},
		},
		
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := twoSum(tt.args.nums, tt.args.target); !reflect.DeepEqual(got, tt.want) {
				t.Errorf("twoSum() = %v, want %v", got, tt.want)
			}
		})
	}
}

