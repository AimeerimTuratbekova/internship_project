package com.custom;

import org.apache.flume.*;
import org.apache.flume.conf.Configurable;
import org.apache.flume.sink.AbstractSink;

import java.io.BufferedWriter;
import java.io.OutputStreamWriter;

public class ExecSink extends AbstractSink implements Configurable {
    private String command;

    @Override
    public void configure(Context context) {
        command = context.getString("command");
    }

    @Override
    public Status process() throws EventDeliveryException {
        Channel ch = getChannel();
        Transaction txn = ch.getTransaction();
        txn.begin();
        try {
            Event event = ch.take();
            if (event == null) {
                txn.commit();
                return Status.BACKOFF;
            }

            Process process = Runtime.getRuntime().exec(command);
            try (BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(process.getOutputStream()))) {
                writer.write(new String(event.getBody()));
                writer.newLine();
                writer.flush();
            }

            int exitCode = process.waitFor();

            if (exitCode != 0) {
                throw new EventDeliveryException("Python script exited with code " + exitCode);
            }

            txn.commit();
            return Status.READY;
        } catch (Exception e) {
            txn.rollback();
            throw new EventDeliveryException("Failed to execute command", e);
        } finally {
            txn.close();
        }
    }
}
