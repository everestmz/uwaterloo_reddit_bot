from tools.s3 import update_json, get_data
from tools.helpers import how_many_comments
from tools.classifier_helpers import print_metrics
from troll_comments import data_builder as troll_builder
from troll_comments import classifier as troll_classifier
from comment_scores.data_builder import generate, cherry_pick_thread, hot_post_stream
from comment_scores.classifier import determine_comment_score

def build_comment_score_data():
    threads = get_data('score', 'threads')
    comments = get_data('score', 'comments')

    while True:
        print "0) Exit"
        print "1) Comment stream [count]"
        print "2) Cherry Pick Thread [thread]"
        print "3) Guess Comment"
        print "4) How many Comments"
        print "5) Get top threads [count]"
        print "6) Metrics"
        response = raw_input("> ").split(' ')
        response[0] = int(response[0])

        result = {"threads": [], "data": []}

        if response[0] == 0:
            break
        elif response[0] == 1:
            result = generate(int(response[1]), threads)
        elif response[0] == 2:
            result = cherry_pick_thread(response[1], threads)
        elif response[0] == 3:
            comment = raw_input("Type the comment > ")
            print determine_comment_score(comments, comment)
        elif response[0] == 4:
            print how_many_comments(comments)
        elif response[0] == 5:
            result = hot_post_stream(threads, int(response[1]))
        elif response[0] == 6:
            print_metrics(comments, ['bernoulli'])
        else:
            continue

        if result != {"threads": [], "data": []}:
            update_json('score', 'comments', result['data'])
            update_json('score', 'threads', result['threads'])


def build_troll_comment_data():
    data = get_data('troll', 'comments')
    threads = get_data('troll', 'threads')

    while True:
        print "0) Exit"
        print "1) Comment Stream [count]"
        print "2) Hot Post Comments [count]"
        print "3) Cherry Pick Thread"
        print "4) Test a phrase"
        print "5) Metrics"
        print "6) Test thread trolliness [thread]"
        print "7) How many Comments"


        selection = raw_input("> ").split(' ')
        selection[0] = int(selection[0])

        final_data = {}

        if selection[0] == 0:
            break
        elif selection[0] == 1:
           final_data = troll_builder.new_comment_loop(int(selection)[1], threads, data)
        elif selection[0] == 2:
            final_data = troll_builder.get_hot_post_comments(int(selection)[1], threads)
        elif selection[0] == 3:
            final_data = troll_builder.cherry_pick_thread(threads)
        elif selection[0] == 4:
            final_data = troll_classifier.classify_cmdline(data)
        elif selection[0] == 5:
            print_metrics(data)
        elif selection[0] == 6:
            print troll_classifier.trolliness(data, selection[1])
        elif selection[0] == 7:
            print how_many_comments(data)
        else:
            continue

        if final_data != {}:
            update_json('troll', 'comments', final_data["data"])
            update_json('troll', 'threads', final_data["threads"])

def main():
    while True:
        print "0) Exit"
        print "1) Troll Comments"
        print "2) Comment Scores"
        selection = int(raw_input("> "))

        if selection == 0:
            exit(0)
        elif selection == 1:
            build_troll_comment_data()
        elif selection == 2:
            build_comment_score_data()

if __name__ == "__main__":
    main()