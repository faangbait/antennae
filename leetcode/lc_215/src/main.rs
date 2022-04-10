pub struct Solution {}

fn main() {
    let sol = Solution::find_kth_largest;
    assert_eq!(sol(vec![3,2,1,5,6,4],2), 5);
    assert_eq!(sol(vec![3,2,3,1,2,4,5,5,6],4), 4);
    
}


impl Solution {
    pub fn find_kth_largest(nums: Vec<i32>, k: i32) -> i32 {
        let mut n = nums.clone();
        *n.select_nth_unstable_by(k as usize - 1,|a,b| b.cmp(a)).1
    }
}
