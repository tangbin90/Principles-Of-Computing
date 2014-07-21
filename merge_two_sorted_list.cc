class Solution {
public:
    ListNode *mergeTwoLists(ListNode *l1, ListNode *l2) {
        if( l1 == NULL )    return l2;
        if( l2 == NULL )    return l1;
        if( l1 -> val == l2 -> val ) {
            ListNode *temp1 = l1 -> next;
            ListNode *temp2 = l2 -> next;
            l1 -> next = l2;
            l2 -> next = mergeTwoLists( temp1,temp2 );
            return l1;
        }
        else if( l1 -> val < l2 -> val )    {
            ListNode *temp = l1 -> next;
            l1 -> next = mergeTwoLists( temp,l2 );
            return l1;
        }
        else
            return mergeTwoLists( l2,l1 );
    }
};