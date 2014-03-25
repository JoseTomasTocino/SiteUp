package com.josetomastocino.siteupclient.app;

import android.widget.ArrayAdapter;
import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import org.w3c.dom.Text;

import java.util.ArrayList;

public class CheckListArrayAdapter extends ArrayAdapter<CheckInList> {
    private final Context context;
    private final ArrayList<CheckInList> values;

    public CheckListArrayAdapter(Context context, ArrayList<CheckInList> values) {
        super(context, R.layout.check_list_item, values);
        this.context = context;
        this.values = values;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        LayoutInflater inflater = (LayoutInflater) context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        View rowView = inflater.inflate(R.layout.check_list_item, parent, false);

        ImageView iconImageView = (ImageView) rowView.findViewById(R.id.icon);
        TextView titleTextView = (TextView) rowView.findViewById(R.id.firstLine);
        TextView descriptionTextView = (TextView) rowView.findViewById(R.id.secondLine);

        titleTextView.setText(values.get(position).getTitle());
        descriptionTextView.setText(values.get(position).getDescription());

        int status = values.get(position).getStatus();
        if (status == 0) {
            iconImageView.setImageResource(R.drawable.ic_siteup_up);
        } else {
            iconImageView.setImageResource(R.drawable.ic_siteup_down);
        }

        /*
        if (s.startsWith("Windows7") || s.startsWith("iPhone") || s.startsWith("Solaris")) {
            imageView.setImageResource(R.drawable.no);
        } else {
            imageView.setImageResource(R.drawable.ok);
        } //*/

        return rowView;
    }
}
