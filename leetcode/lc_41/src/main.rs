fn main() {
    println!("{}", Solution::first_missing_positive(vec![1,2,0]));
    println!("{}", Solution::first_missing_positive(vec![4,3,4,1,1,4,1,4]));
    
}

pub struct Solution {}

impl Solution {
    pub fn first_missing_positive(nums: Vec<i32>) -> i32 {

        let mut arr = nums.clone();
        arr.retain(|x| *x > 0);
        arr.sort_unstable();
        let mut lowest = 1;

        for elem in arr {
            if elem == lowest { lowest += 1 } else if elem > lowest { return lowest }
        }
        return lowest 
        
    }
}
