# -*- coding: utf-8 -*-
from . import models

# <!-- Warning banner on the cancelled original -->
#             <xpath expr="//sheet" position="before">
#                 <div
#                     class="alert alert-warning mb-0"
#                     role="alert"
#                     invisible="split_order_count == 0"
#                 >
#                     This order was split into
#                     <strong><field name="split_order_count" readonly="1" nolabel="1"/></strong>
#                     vendor-specific POs on confirmation.
#                     Use the <strong>Split Orders</strong> button to view them.
#                 </div>
#
#                 <!-- Info banner on each split child -->
#                 <div
#                     class="alert alert-info mb-0"
#                     role="alert"
#                     invisible="not is_split_order"
#                 >
#                     This is a <strong>split purchase order</strong> generated from
#                     <field name="original_order_id" readonly="1" nolabel="1"/>.
#                 </div>
#             </xpath>
