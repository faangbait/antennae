fn main() {
    Solution::find_closest_number(vec![-4,-2,1,4,8]);
}
pub struct Solution {}
impl Solution {
    pub fn find_closest_number(nums: Vec<i32>) -> i32 {
        let mut n = nums.clone();
        let lowest = n.select_nth_unstable_by_key(0, |n| n.abs()).1;

        
        if lowest > &mut 0 {
            return *lowest;
        } else {
            if nums.contains(&(*lowest* -1)) {
                return *lowest*-1
            } else {
                return *lowest;
            }
            
        };
    }
}
