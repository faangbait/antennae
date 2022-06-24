pub struct Solution {}

fn main() {}


impl Solution {
    pub fn find_kth_largest(nums: Vec<i32>, k: i32) -> i32 {
        let mut n = nums.clone();
        *n.select_nth_unstable_by(k as usize - 1,|a,b| b.cmp(a)).1
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    pub fn simple() {
        assert_eq!(Solution::find_kth_largest(vec![3,2,1,5,6,4],2), 5);
        assert_eq!(Solution::find_kth_largest(vec![3,2,3,1,2,4,5,5,6],4), 4);
    }
}
