<template>
    <div>
        <Alert :message="message" :variant="status" />
        <Alert v-if="viewOnly" message="Not implemented" variant="dark" />
        <Alert v-else-if="loading" message="Waiting for data" variant="info" />
        <div v-else-if="dataManagers && !dataManagers.length">
            <Alert variant="primary">
                <h4 class="alert-heading">None installed</h4>
                You do not currently have any Data Managers installed.
            </Alert>
        </div>
        <div v-else-if="dataManagers && dataTables">
            <b-container fluid>
                <b-row>
                    <b-col md="6">
                        <b-form-group description="Search for strings or regular expressions">
                            <b-input-group>
                                <b-form-input
                                    v-model="filter"
                                    placeholder="Type to Search"
                                    @keyup.esc.native="filter = ''" />
                                <b-input-group-append>
                                    <b-btn :disabled="!filter" @click="filter = ''">Clear (esc)</b-btn>
                                </b-input-group-append>
                            </b-input-group>
                        </b-form-group>
                    </b-col>
                </b-row>
            </b-container>
            <b-card-group columns>
                <b-card no-body header="Installed Data Managers" id="data-managers-card">
                    <b-list-group flush>
                        <b-list-group-item v-for="(dataManager, index) in dataManagersFiltered" :key="index">
                            <b-button-group vertical>
                                <b-button
                                    :href="dataManager['toolUrl']"
                                    target="_blank"
                                    variant="primary"
                                    :id="kebabCase(dataManager['name'])">
                                    <div>{{ dataManager["name"] }}</div>
                                    <div v-if="dataManager['description']">
                                        <i>{{ dataManager["description"] }}</i>
                                    </div>
                                </b-button>
                                <b-button
                                    :to="{
                                        name: 'DataManagerJobs',
                                        params: { id: encodeURIComponent(dataManager['id']) },
                                    }"
                                    :id="kebabCase(dataManager['name']) + '-jobs'">
                                    Jobs
                                </b-button>
                            </b-button-group>
                        </b-list-group-item>
                    </b-list-group>
                </b-card>
                <b-card no-body header="Tool Data Tables">
                    <b-list-group flush>
                        <b-list-group-item
                            v-for="(dataTable, index) in dataTablesFiltered"
                            :key="index"
                            :to="{ name: 'DataManagerTable', params: { name: dataTable['name'] } }"
                            :id="kebabCase(dataTable['name']) + '-table'"
                            :variant="dataTable['managed'] === true ? 'primary' : 'link'">
                            {{ dataTable["name"] }}
                            <b-badge v-if="dataTable['managed'] === true" variant="primary" pill
                                ><span class="fa fa-exchange"
                            /></b-badge>
                        </b-list-group-item>
                    </b-list-group>
                </b-card>
            </b-card-group>
        </div>
    </div>
</template>

<script>
import { getAppRoot } from "onload/loadConfig";
import axios from "axios";
import Alert from "components/Alert.vue";
import { debounce } from "underscore";

export default {
    components: {
        Alert,
    },
    props: {
        debouncePeriod: { type: Number, required: false, default: 100 },
    },
    data() {
        return {
            dataManagers: [],
            dataTables: [],
            filter: "",
            viewOnly: false,
            message: "",
            status: "",
            loading: false,
        };
    },
    computed: {
        dataManagersFiltered() {
            return this.dataManagers.filter((d) => d["name"].match(new RegExp(this.filter, "i")));
        },
        dataTablesFiltered() {
            return this.dataTables.filter((d) => d["name"].match(new RegExp(this.filter, "i")));
        },
    },
    methods: {
        kebabCase(s) {
            return s.toLowerCase().replace(/ /g, "-");
        },
        load() {
            this.loading = true;
            axios
                .get(`${getAppRoot()}data_manager/data_managers_list`)
                .then((response) => {
                    console.log("response", response);
                    this.dataManagers = response.data.dataManagers;
                    this.dataTables = response.data.dataTables;
                    this.viewOnly = response.data.viewOnly;
                    this.message = response.data.message;
                    this.status = response.data.status;
                })
                .catch((error) => {
                    console.error(error);
                })
                .finally(() => {
                    this.loading = false;
                });
        },
    },
    created() {
        console.log("created");
        this.debouncedLoad = debounce(this.load, this.debouncePeriod);
        this.debouncedLoad();
    },
    beforeRouteEnter(to, from, next) {
        console.log("beforeRouteEnter");
        next((vm) => vm.debouncedLoad());
    },
};
</script>
