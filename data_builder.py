from tools.helpers import bulk_add_to_data, load_json_into_array
from troll_comments import data_builder as troll

def build_troll_comment_data():
    data = load_json_into_array('troll_comments/troll_training_data.json')['comments']
    threads = load_json_into_array('troll_comments/threads.json')['threads']

    while True:
        print "0) Exit"
        print "1) Comment Stream [count]"
        print "2) Hot Post Comments [count]"
        print "3) Cherry Pick Thread"

        selection = raw_input("> ").split(' ')

        final_data = 0

        if selection[0] == 0:
            exit(0)
        elif selection[0] == 1:
           final_data = troll.new_comment_loop(selection[1], threads, data)
        elif selection[0] == 2:
            final_data = troll.get_hot_post_comments(selection[1], threads)
        elif selection[0] == 3:
            final_data = troll.cherry_pick_thread(threads)

        bulk_add_to_data("troll_comments/troll_training_data.json", 'comments', final_data['data'])
        bulk_add_to_data("troll_comments/threads.json", 'threads', final_data['threads'])

def main():
    build_troll_comment_data()


if __name__ == "__main__":
    main()