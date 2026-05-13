/** @odoo-module **/
import {renderToElement} from "@web/core/utils/render";
import publicWidget from "@web/legacy/js/public/public_widget";
import {rpc} from "@web/core/network/rpc";


publicWidget.registry.get_product_tab = publicWidget.Widget.extend({
    selector: '.categories_section',
    async willStart() {
        const result = await rpc('/get_product_categories', {});
        const dynamic_id = await rpc('/random_number_generator',{});

        if (result && result.categories.length > 0) {
            const chunks = [];
            for (let i = 0; i < result.categories.length; i += 4) {
                chunks.push(result.categories.slice(i, i + 4));
            }
            if (chunks.length > 0){
                chunks[0].is_active = true;
            }

            this.chunks = chunks;
            this.result = result;
            this.dynamic_id = dynamic_id
        }

    },

    start() {
        if (this.result) {
            this.$target.empty().html(renderToElement('library_management.category_data', {
                result: this.result,
                chunks: this.chunks,
                dynamic_id: this.dynamic_id,
            }))
        }
    },
});
