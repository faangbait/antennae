#[derive(PartialEq, Eq, Clone, Debug)]
pub struct ListNode {
    pub val: i32,
    pub next: Option<Box<ListNode>>,
}

impl ListNode {
    #[inline]
    fn new(val: i32) -> Self {
        ListNode { next: None, val }
    }
}

pub struct Solution {}

impl Solution {
    /// You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order,
    /// and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.
    pub fn add_two_numbers(
        l1: Option<Box<ListNode>>,
        l2: Option<Box<ListNode>>,
    ) -> Option<Box<ListNode>> {
        
        let mut l1 = l1;
        let mut l2 = l2;

        let mut head = Box::new(ListNode::new(0));
        let mut current = &mut head;
        
        // Iterate through the ListNodes and build a LL
        while l1.is_some() || l2.is_some() {
            let mut carry = 0;

            // Advance l1
            if let Some(node) = l1 {
                current.val += node.val;
                l1 = node.next;
            };

            // Advance l2
            if let Some(node) = l2 {
                current.val += node.val;
                l2 = node.next;
            };

            // Set our carries
            while current.val >= 10 {
                current.val -= 10;
                carry += 1;
            }

            // Advance our answer list, adding carry as the new value
            if l1.is_some() || l2.is_some() || carry > 0{
                current.next = Some(Box::new(ListNode::new(carry)));
            }

            // Move the current pointer to the next node
            if current.next.is_some() {
                current = current.next.as_mut().expect("head.next is None");
            }
        }
        
        Some(head)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    pub fn zeros() {
        let l1 = Some(Box::new(ListNode {
            val: 0,
            next: None
        }));
        let l2 = Some(Box::new(ListNode {
            val: 0,
            next: None
        }));
        let l3 = Some(Box::new(ListNode {
            val: 0,
            next: None
        }));
        
        assert_eq!(Solution::add_two_numbers(l1, l2), l3);
    }

    #[test]
    pub fn simple() {
        let l1 = Some(Box::new(ListNode {
            val: 2,
            next: Some(Box::new(ListNode {
                val: 4,
                next: Some(Box::new(ListNode {
                    val: 3,
                    next: None,
                })),
            })),
        }));

        let l2 = Some(Box::new(ListNode {
            val: 5,
            next: Some(Box::new(ListNode {
                val: 6,
                next: Some(Box::new(ListNode {
                    val: 4,
                    next: None,
                })),
            })),
        }));

        let l3 = Some(Box::new(ListNode {
            val: 7,
            next: Some(Box::new(ListNode {
                val: 0,
                next: Some(Box::new(ListNode {
                    val: 8,
                    next: None,
                })),
            })),
        }));

        assert_eq!(Solution::add_two_numbers(l1, l2), l3);
    }

    #[test]
    pub fn multicarry() {

        let l1 = Some(Box::new(ListNode {
            val: 9,
            next: Some(Box::new(ListNode {
                val: 9,
                next: Some(Box::new(ListNode {
                    val: 9,
                    next: Some(Box::new(ListNode {
                        val: 9,
                        next: Some(Box::new(ListNode {
                            val: 9,
                            next: Some(Box::new(ListNode {
                                val: 9,
                                next: Some(Box::new(ListNode {
                                    val: 9,
                                    next: None
                                })),
                            })),
                        })),
                    })),
                })),
            })),
        }));

        let l2 = Some(Box::new(ListNode {
            val: 9,
            next: Some(Box::new(ListNode {
                val: 9,
                next: Some(Box::new(ListNode {
                    val: 9,
                    next: Some(Box::new(ListNode { val: 9, next: None })),
                })),
            })),
        }));

        let l3 = Some(Box::new(ListNode {
            val: 8,
            next: Some(Box::new(ListNode {
                val: 9,
                next: Some(Box::new(ListNode {
                    val: 9,
                    next: Some(Box::new(ListNode {
                        val: 9,
                        next: Some(Box::new(ListNode {
                            val: 0,
                            next: Some(Box::new(ListNode {
                                val: 0,
                                next: Some(Box::new(ListNode {
                                    val: 0,
                                    next: Some(Box::new(ListNode { val: 1, next: None }))
                                }))
                            }))
                        }))
                    })),
                }))
            }))
        }));

        assert_eq!(Solution::add_two_numbers(l1, l2), l3);

    }
}

fn main() {}
