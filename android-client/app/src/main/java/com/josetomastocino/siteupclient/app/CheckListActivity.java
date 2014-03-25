package com.josetomastocino.siteupclient.app;

import android.content.Intent;
import android.net.Uri;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ListView;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;


public class CheckListActivity extends ActionBarActivity {

    private JSONObject mCheckData;
    private ArrayList<CheckInList> mChecks;

    private ListView mListView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_check_list);

        mListView = (ListView) findViewById(R.id.listView);

        // Initialise list of checks
        mChecks = new ArrayList<CheckInList>();

        String receivedData = getIntent().getExtras().getString("received_data");

        try {
            mCheckData = new JSONObject(receivedData);

            JSONArray array = mCheckData.getJSONArray("groups");

            // Loop over the user groups
            for (int i = 0; i < array.length(); i++) {
                JSONObject currentGroup = array.getJSONObject(i);
                Log.i("WAT", currentGroup.getString("title"));

                // Loop over the group's checks
                JSONArray checksArray = currentGroup.getJSONArray("checks");
                for (int j = 0; j < checksArray.length(); j++) {
                    JSONObject currentCheckJson = checksArray.getJSONObject(j);

                    CheckInList currentCheck = new CheckInList();
                    currentCheck.setTitle(currentCheckJson.getString("title"));
                    currentCheck.setDescription(currentCheckJson.getString("description"));
                    currentCheck.setURL(currentCheckJson.getString("detail_url"));
                    currentCheck.setStatus(currentCheckJson.getInt("status"));

                    mChecks.add(currentCheck);
                }
            }
        } catch (JSONException e) {
            // no-op nigga
        }

        CheckListArrayAdapter adapter = new CheckListArrayAdapter(this, mChecks);
        mListView.setAdapter(adapter);

        mListView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> adapterView, View view, int i, long l) {
                Uri uri = Uri.parse(mChecks.get(i).getURL());
                Intent intent = new Intent(Intent.ACTION_VIEW, uri);
                startActivity(intent);
            }
        });
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
