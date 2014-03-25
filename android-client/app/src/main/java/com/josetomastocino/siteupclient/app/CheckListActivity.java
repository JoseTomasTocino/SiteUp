package com.josetomastocino.siteupclient.app;

import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;


public class CheckListActivity extends ActionBarActivity {

    private JSONObject mCheckData;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_check_list);

        String receivedData = getIntent().getExtras().getString("received_data");

        try {
            mCheckData = new JSONObject(receivedData);

            JSONArray array = mCheckData.getJSONArray("groups");

            for (int i = 0; i < array.length(); i++) {
                Log.i("WAT", array.getJSONObject(i).getString("title"));
            }
        } catch (JSONException e) {
            // no-op nigga
        }
    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.check_list, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();
        if (id == R.id.action_settings) {
            return true;
        }
        return super.onOptionsItemSelected(item);
    }

}
