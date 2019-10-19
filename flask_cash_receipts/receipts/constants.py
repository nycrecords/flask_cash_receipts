ITEM_ROW = """
    <div class="form-group row">
        <label class="col-md-4 control-label" for="username">{{item_name}}</label>
        <div class="col-md-2">
            <button type="button" id="add{{item_id}}">Add</button>
        </div>
        <div class="col-md-2">
            <button type="button" id="remove{{item_id}}">Add</button>
        </div>
        <div class="col-md-2">
            <input id="{{item_id}}Count" name="{{item_id}}" type="text" placeholder="0"
                class="form-control input-md" required=" disabled />
        </div>
    </div>
    """
