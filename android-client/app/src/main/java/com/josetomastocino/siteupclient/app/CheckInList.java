package com.josetomastocino.siteupclient.app;

public class CheckInList {
    private String mTitle;
    private String mDescription;
    private int mStatus;
    private String mURL;

    public CheckInList(){

    }

    public String getTitle() {
        return mTitle;
    }

    public void setTitle(String mTitle) {
        this.mTitle = mTitle;
    }

    public String getDescription() {
        return mDescription;
    }

    public void setDescription(String mDescription) {
        this.mDescription = mDescription;
    }

    public int getStatus() {
        return mStatus;
    }

    public void setStatus(int mStatus) {
        this.mStatus = mStatus;
    }

    public String getURL() {
        return mURL;
    }

    public void setURL(String mURL) {
        this.mURL = mURL;
    }
}
