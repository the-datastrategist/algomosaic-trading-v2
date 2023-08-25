#!/usr/bin/env python

DATE = 'ticker_time'


class modelPlots():

    def __init__(self, modelObject):
        self.predictions = modelObject._get_predictions_or_evaluations()

    def _get_plot_data(self, output_type, start_date=None, end_date=None):
        """Get prediction based on output type"""
        if "pred" in output_type:
            output_data = self.predictions[
                [DATE, 'predictions', 'outcomes']].sort_values(by=DATE)
        elif "error" in output_type:
            output_data = self.predictions[
                [DATE, 'errors']].sort_values(by=DATE)

        # index and filter on date
        output_data = output_data.set_index(DATE)
        start_date = start_date or str(output_data.index.min())
        end_date = end_date or str(output_data.index.max())
        output_data = output_data[start_date:end_date]
        return output_data

    def plot_predictions_by_date(self, start_date=None, end_date=None):
        # get prediction data
        preds_by_date = self._get_plot_data(
            'predictions', start_date, end_date)
        print("""PLOT: Predictions by Date
        `self.plot_predictions_by_date(start_date, end_date)`""")
        return preds_by_date.plot(kind='bar', figsize=(20, 5))

    def plot_errors_by_date(self, start_date=None, end_date=None):
        # get prediction data
        errors_by_date = self._get_plot_data(
            'errors', start_date, end_date)
        print("""PLOT: Prediction Errors by Date`""")
        return errors_by_date.plot(kind='bar', figsize=(20, 5))

    def plot_predictions_histogram(
        self,
        start_date=None,
        end_date=None,
        bins=30
    ):
        preds_histogram = self._get_plot_data(
            'predictions', start_date, end_date)
        print("""PLOT: Predictions Histogram""")
        return preds_histogram.plot.hist(bins=bins, alpha=0.5, figsize=(10, 5))

    def plot_errors_histogram(
        self,
        start_date=None,
        end_date=None,
        bins=30
    ):
        errors_histogram = self._get_plot_data('errors', start_date, end_date)
        print("""PLOT: Predictions Histogram""")
        return errors_histogram.plot.hist(
            bins=bins, alpha=0.5, figsize=(10, 5))

    def plot_predictions_scatterplot(
        self,
        start_date=None,
        end_date=None
    ):
        # get prediction data
        preds_by_date = self._get_plot_data(
            'predictions', start_date, end_date)
        preds_by_date = preds_by_date.reset_index()
        preds_by_date = preds_by_date[
            ['outcomes', 'predictions']].astype('float64')
        print("""PLOT: Predictions by Date""")
        return preds_by_date.plot.scatter(
            x='outcomes', y='predictions', figsize=(5, 5))
