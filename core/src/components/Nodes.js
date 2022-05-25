import { LiteGraph } from "litegraph.js";

export function EndpointVariable() {
    this.boxcolor = "blue"
    this.widgets_up = true;
    this.addWidget("text", "name", "", (val) => this.title = val)

    this.addOutput("connection", "text");
    this.onExecute = function () {
        var name = this.getInputData(0);
        this.setOutputData(0, name);
    }

    this.onSelected = function () {
        console.log("eooo")
    }
}

export function Net() {
    this.addOutput("name", "text");
    this.addProperty("name", "");
    this.widget = this.addWidget("text", "name", "", "name");
    this.widgets_up = true;
    this.size = [180, 30];
    this.boxcolor = "red"
    this.desc = "Docker net";

    this.setName = function (v) {
        this.setProperty("name", v);
    }

    this.getTitle = function () {
        if (this.flags.collapsed) {
            return this.properties.name;
        }
        return this.title;
    };

    this.onExecute = function () {
        this.setOutputData(0, this.properties["name"]);
    };

    this.onDrawBackground = function (ctx) {
        //show the current name
        this.outputs[0].label = this.properties["name"];
    };
}


//Input for a subgraph
export function Container() {
    this.addOutput("", "number");

    this.name_in_graph = "";
    this.properties = {
        name: "",
        type: "number",
        value: 0
    };

    var that = this;

    this.name_widget = this.addWidget(
        "text",
        "Name",
        this.properties.name,
        function (v) {
            if (!v) {
                return;
            }
            that.setProperty("name", v);
        }
    );
    this.type_widget = this.addWidget(
        "text",
        "Type",
        this.properties.type,
        function (v) {
            that.setProperty("type", v);
        }
    );

    this.value_widget = this.addWidget(
        "number",
        "Value",
        this.properties.value,
        function (v) {
            that.setProperty("value", v);
        }
    );

    this.widgets_up = true;
    this.size = [180, 90];


    this.title = "Input";
    this.desc = "Input of the graph";

    this.onConfigure = function () {
        this.updateType();
    }

    //ensures the type in the node output and the type in the associated graph input are the same
    this.updateType = function () {
        var type = this.properties.type;
        this.type_widget.value = type;

        //update output
        if (this.outputs[0].type != type) {
            if (!LiteGraph.isValidConnection(this.outputs[0].type, type))
                this.disconnectOutput(0);
            this.outputs[0].type = type;
        }

        //update widget
        if (type == "number") {
            this.value_widget.type = "number";
            this.value_widget.value = 0;
        }
        else if (type == "boolean") {
            this.value_widget.type = "toggle";
            this.value_widget.value = true;
        }
        else if (type == "string") {
            this.value_widget.type = "text";
            this.value_widget.value = "";
        }
        else {
            this.value_widget.type = null;
            this.value_widget.value = null;
        }
        this.properties.value = this.value_widget.value;

        //update graph
        if (this.graph && this.name_in_graph) {
            this.graph.changeInputType(this.name_in_graph, type);
        }
    }

    //this is executed AFTER the property has changed
    this.onPropertyChanged = function (name, v) {
        if (name == "name") {
            if (v == "" || v == this.name_in_graph || v == "enabled") {
                return false;
            }
            if (this.graph) {
                if (this.name_in_graph) {
                    //already added
                    this.graph.renameInput(this.name_in_graph, v);
                } else {
                    this.graph.addInput(v, this.properties.type);
                }
            } //what if not?!
            this.name_widget.value = v;
            this.name_in_graph = v;
        }
        else if (name == "type") {
            this.updateType();
        }
        else if (name == "value") {
        }
    }

    this.getTitle = function () {
        if (this.flags.collapsed) {
            return this.properties.name;
        }
        return this.title;
    };

    this.onAction = function (action, param) {
        if (this.properties.type == LiteGraph.EVENT) {
            this.triggerSlot(0, param);
        }
    };

    this.onExecute = function () {
        var name = this.properties.name;
        //read from global input
        var data = this.graph.inputs[name];
        if (!data) {
            this.setOutputData(0, this.properties.value);
            return;
        }

        this.setOutputData(0, data.value !== undefined ? data.value : this.properties.value);
    };


    this.onRemoved = function () {
        if (this.name_in_graph) {
            this.graph.removeInput(this.name_in_graph);
        }
    };
}
