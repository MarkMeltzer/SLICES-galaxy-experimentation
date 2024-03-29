<template>
    <span itemprop="creator" itemscope itemtype="https://schema.org/Organization">
        <font-awesome-icon ref="button" icon="building" />
        <b-popover
            triggers="click blur"
            :placement="hoverPlacement"
            :target="this.$refs['button'] || 'works-lazily'"
            title="Organization">
            <b-table striped :items="items"> </b-table>
        </b-popover>
        <span v-if="name">
            <span itemprop="name">{{ name }}</span>
            <span v-if="email">
                (<span itemprop="email" :content="organization.email">{{ email }}</span
                >)
            </span>
        </span>
        <span itemprop="email" :content="organization.email" v-else-if="email">
            {{ email }}
        </span>
        <a v-if="url" :href="url" target="_blank">
            <link itemprop="url" :href="url" />
            <font-awesome-icon v-b-tooltip.hover title="Organization URL" icon="external-link-alt" />
        </a>
        <meta
            v-for="attribute in explicitMetaAttributes"
            :key="attribute.attribute"
            :itemprop="attribute.attribute"
            :content="attribute.value" />
        <slot name="buttons"></slot>
    </span>
</template>

<script>
import ThingViewerMixin from "./ThingViewerMixin";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";

// maybe faUsers instead of faBuilding?
import { faExternalLinkAlt, faBuilding } from "@fortawesome/free-solid-svg-icons";

library.add(faExternalLinkAlt, faBuilding);

export default {
    mixins: [ThingViewerMixin],
    components: {
        FontAwesomeIcon,
    },
    props: {
        organization: {
            type: Object,
        },
        hoverPlacement: {
            type: String,
            default: "left",
        },
    },
    data() {
        return {
            implicitMicrodataProperties: ["name", "email", "url", "identifier"],
            thing: this.organization,
        };
    },
    computed: {
        name() {
            return this.organization.name;
        },
    },
};
</script>
