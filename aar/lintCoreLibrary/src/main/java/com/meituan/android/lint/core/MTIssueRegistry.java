package com.meituan.android.lint.core;

import com.android.tools.lint.client.api.IssueRegistry;
import com.android.tools.lint.detector.api.Issue;

import java.util.Arrays;
import java.util.List;

public class MTIssueRegistry extends IssueRegistry {
    @Override
    public synchronized List<Issue> getIssues() {
        System.out.println("==== MT lint start ====");
        return Arrays.asList(
                LogDetector.ISSUE,
                HashMapForJDK7Detector.ISSUE
        );
    }
}
